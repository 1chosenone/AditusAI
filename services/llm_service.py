"""LLM service for candidate information extraction."""

from datetime import datetime
import logging
from core.config import settings
import instructor
from instructor.exceptions import (
    IncompleteOutputException,
    InstructorRetryException,
    ResponseParsingError,
)
from litellm import acompletion
from exceptions import ResumeParsingError
from schemas.candidate import CandidateSchema
from schemas.pdf import PDFContent

logger = logging.getLogger(__name__)

client = instructor.from_litellm(acompletion)


def _get_system_prompt() -> str:
    """Generate the system prompt for resume parsing.

    Returns:
        System prompt string containing instructions for the LLM on how to
        parse and extract candidate information from resumes.
    """
    now = datetime.now()

    return f"""You are a high-precision Resume Parsing Engine. 

    <CURRENT_DATE>
    - Today is {now.year}-{now.month}-{now.day}
    </CURRENT_DATE>

    Your role is to interpret unstructured text and map it to the provided data schema using the following logic:
    
    <TEMPORAL_REASONING>
        - For every education or role, compare the end date with CURRENT_DATE.
        - If end_date < CURRENT_DATE, the item is completed → use past tense.
        - If end_date >= CURRENT_DATE or "Present" → ongoing → use present tense.
        - NEVER describe completed items as "currently", "in progress", or "ongoing".
    </TEMPORAL_REASONING>
    
    <BIO_SYNTHESIS>
        - Generate a two-sentence career generalization.
        - Weight recent roles and current seniority more heavily, but synthesize the overall career arc and long-term skill growth.
        - Avoid simply listing the last job; capture the candidate's professional identity.
        - Use TEMPORAL_REASONING to correctly determine tense for each education and role.
        <EXAMPLE>
            CONTEXT: Today is March 17, 2026. 
            INPUT: "Stage at OODA, Jan-Apr 2025. B.Eng Graduation: Oct 2025."
            
            BAD OUTPUT: "Student currently completing a degree and interning at OODA..."
            GOOD OUTPUT: "Software engineer and B.Eng graduate with professional experience in defense-sector backend development at OODA Technologies..."
            
            REASONING: Since Oct 2025 is before March 2026, the status is "Graduate," not "Student."
        </EXAMPLE>
    </BIO_SYNTHESIS>

    <SKILL_PROFICENCY_LOGIC>
        - DEFAULT: Map proficiency to "Intermediate" if not explicitly stated.
        - INFERENCE: Elevate to "Advanced" or "Expert" if the skill is used across multiple roles or associated with high-complexity architectural/leadership tasks.
    </SKILL_PROFICENCY_LOGIC>

    <EXTRACTION_RULES>
        - DATA INTEGRITY: Never hallucinate; extract exactly as written unless inference is specifically requested.
        - JOB_TYPE: Map non-standard terms to professional equivalents (e.g., "Stage" -> "Internship").
        - GEOGRAPHY: Use ISO abbreviations for Regions (QC, ON, NY) and infer Country from City/Region if missing.
        - TEMPORAL: 
            1. Extract YEARS only. Ignore months/days.
            2. If a range is within the same year (e.g., "Jan 2025 - April 2025"), both start_year and end_year MUST be that year (2025). 
            3. Do NOT default end_year to null if an end date is explicitly mentioned in the text. 
            4. Only use null for end_year if the text explicitly says "Present", "Current", or "To date".
    </EXTRACTION_RULES>
    """


async def extract_candidate_info(resume: PDFContent) -> CandidateSchema:
    """Extract candidate information from resume content using LLM.

    Args:
        resume: PDFContent containing the resume text and hyperlinks.

    Returns:
        CandidateSchema with extracted candidate information.

    Raises:
        RuntimeError: If all retries are exhausted or an unexpected error occurs.
        IncompleteOutputException: If the LLM output is truncated.
        ResponseParsingError: If the response cannot be parsed.
    """
    logger.debug("Extracting candidate informations from the resume...")

    try:
        candidate_data, response = await client.chat.completions.create_with_completion(
            model=settings.llm_model_name,
            response_model=CandidateSchema,
            messages=[
                {
                    "role": "system",
                    "content": _get_system_prompt(),
                },
                {
                    "role": "user",
                    "content": f"Resume:\n{resume.text}\n\nLinks:\n{resume.hyperlinks}",
                },
            ],
            max_retries=settings.llm_max_tries,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
        )
    except InstructorRetryException as e:
        logger.error("All %s retries exhausted:", e.n_attempts)
        for attempt in e.failed_attempts:
            logger.error("Error: %s", attempt.exception())
        raise ResumeParsingError(
            "Failed to extract candidate info after retries"
        ) from e
    except IncompleteOutputException as e:
        raise ResumeParsingError(
            "LLM has probably hits the max_tokens limit before completing its "
            "response. Output truncated. Partial data: %s",
            e.last_completion,
        ) from e
    except ResponseParsingError as e:
        raise ResumeParsingError("Failed to parse response in %s mode", e.mode) from e
    except Exception as e:
        raise ResumeParsingError(
            "Unexpected error while extracting candidate info from the resume PDF"
        ) from e
    finally:
        logger.info("Finished extracting candidate info from the resume")

        if response:
            finish_reason = response.choices[0].finish_reason
            usage = response.usage

            logger.debug(
                "LLM call finished — model: %s | stop: %s | tokens: %s in / %s out / %s total",
                response.model,
                finish_reason,
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.total_tokens,
            )

    return candidate_data
