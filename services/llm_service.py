"""LLM service for candidate information extraction."""

from datetime import datetime
from functools import lru_cache
import logging
import instructor
from instructor.exceptions import (
    IncompleteOutputException,
    InstructorRetryException,
    ResponseParsingError,
)
from litellm import acompletion
from core.config import settings
from exceptions import ResumeParsingError, QueryOptimizationError
from schemas.candidate import CandidateProfileSchema
from schemas.query import OptimizedQuery
from schemas.pdf import PDFContent

logger = logging.getLogger(__name__)


def _get_resume_parsing_system_prompt() -> str:
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
            5. If a month is explicitly mentioned for a date (start or end), whether as a number (e.g., "03"), full name (e.g., "March"), or abbreviation (e.g., "Mar"), extract it and convert it to its numeric form (1-12). Apply this independently: populate start_month and/or end_month only when the corresponding month is provided. If a month is missing for one side, set only that field to null.
    </EXTRACTION_RULES>
    """


def _get_query_optimization_system_prompt(n: int) -> str:
    """Generate the system prompt for query optimization.

    Args:
        n: Number of optimized search terms to generate.

    Returns:
        System prompt string containing instructions for the LLM on how to
        optimize job search queries.
    """

    return f"""You are a Job Search Query Optimization Engine.

    Your role is to receive raw job search terms from a candidate and return exactly {n} optimized search terms.

    <TASK>
        - INPUT: A raw string of job search terms provided by the candidate (e.g., "ai fullstack").
        - OUTPUT: A list of exactly {n} optimized search terms.
    </TASK>

    <OPTIMIZATION_MODES>
        Count the number of terms in the INPUT. Compare that count with N ({n}).

        <REFINEMENT_MODE condition="N <= number of input terms">
            - ONLY refine and expand the terms explicitly provided.
            - Do NOT infer or add unrelated terms.
            - Focus on making each term more professional and searchable.
            <EXAMPLE>
                INPUT: "ai fullstack" (2 terms), N=2
                OUTPUT: ["Artificial Intelligence (AI)", "Full-Stack Developer"]
            </EXAMPLE>
        </REFINEMENT_MODE>

        <EXPANSION_MODE condition="N > number of input terms">
            - Start by refining the provided terms (as in REFINEMENT_MODE).
            - Fill the remaining slots with semantically related terms a recruiter would use.
            - Expand across related technologies, roles, and specializations.
            - Prioritize terms commonly found in job postings.
            <EXAMPLE>
                INPUT: "ai fullstack" (2 terms), N=6
                OUTPUT: ["Artificial Intelligence (AI)", "Full-Stack Developer", "Machine Learning Engineer", "LLM Engineer", "Backend Developer", "Frontend Developer"]
                REASONING: 2 input terms refined first, then 4 related terms inferred to reach N=6.
            </EXAMPLE>
        </EXPANSION_MODE>
    </OPTIMIZATION_MODES>

    <RULES>
        - OUTPUT exactly {n} terms — no more, no less.
        - Use professional, recruiter-friendly terminology.
        - Avoid redundancy — each term must be meaningfully distinct.
        - Preserve the candidate's intent — never replace their terms with unrelated ones.
        - Do NOT include explanations, preamble, or commentary — only the list.
    </RULES>
    """


@lru_cache(maxsize=4)
def _get_client(model_name: str) -> instructor.AsyncInstructor:
    """Create and cache an instructor client for the specified model.

    Args:
        model_name: The name of the LLM model to use.

    Returns:
        An AsyncInstructor client configured for the given model.
    """
    mode = (
        instructor.Mode.JSON
        if model_name.startswith("ollama/")
        else instructor.Mode.TOOLS
    )
    client = instructor.from_litellm(acompletion, mode=mode)
    logger.debug("Instructor/LiteLLM client created")
    return client


async def extract_candidate_info(resume: PDFContent) -> CandidateProfileSchema:
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
        # Retrieve appropriate llm config
        cfg = settings.parsing_llm

        # Get the appropriate instructor client (based on the model)
        client = _get_client(cfg.model)

        candidate_data, response = await client.chat.completions.create_with_completion(
            model=cfg.model,
            response_model=CandidateProfileSchema,
            messages=[
                {
                    "role": "system",
                    "content": _get_resume_parsing_system_prompt(),
                },
                {
                    "role": "user",
                    "content": f"Resume:\n{resume.text}\n\nLinks:\n{resume.hyperlinks}",
                },
            ],
            max_retries=cfg.max_tries,
            max_tokens=cfg.max_tokens,
            temperature=cfg.temperature,
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


async def optimize_query(q: str, terms_to_generate: int = 5):
    """Optimize a job search query using LLM to generate refined search terms.

    Args:
        q: Raw job search terms input by the candidate.
        terms_to_generate: Number of optimized terms to generate (default: 5).

    Returns:
        OptimizedQuery containing the list of refined search terms.

    Raises:
        QueryOptimizationError: If all retries are exhausted or an unexpected error occurs.
    """
    logger.debug("Optimizing jobs search query with AI...")

    try:
        # Retrieve appropriate llm config
        cfg = settings.query_optimization_llm

        # Get the appropriate instructor client (based on the model)
        client = _get_client(cfg.model)

        (
            optimized_query,
            response,
        ) = await client.chat.completions.create_with_completion(
            model=cfg.model,
            response_model=OptimizedQuery,
            messages=[
                {
                    "role": "system",
                    "content": _get_query_optimization_system_prompt(terms_to_generate),
                },
                {
                    "role": "user",
                    "content": q,
                },
            ],
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            max_retries=cfg.max_tries,
            api_base=cfg.api_base,  # None is ignored by litellm for cloud providers
        )
    except InstructorRetryException as e:
        logger.error("All %s retries exhausted:", e.n_attempts)
        for attempt in e.failed_attempts:
            logger.error("Error: %s", attempt.exception())
        raise QueryOptimizationError(
            "Failed to optimize the query after retries"
        ) from e
    except IncompleteOutputException as e:
        raise QueryOptimizationError(
            "LLM has probably hits the max_tokens limit before completing its "
            "response. Output truncated. Partial data: %s",
            e.last_completion,
        ) from e
    except Exception as e:
        raise QueryOptimizationError(
            "Unexpected error while optimizing the query"
        ) from e
    finally:
        logger.info("Finished optimizing query")

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

    return optimized_query
