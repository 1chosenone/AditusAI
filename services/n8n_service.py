"""Service for interacting with n8n webhooks."""

import httpx
from core.config import settings
from schemas.query import JobSearchQuery


async def trigger_job_search(query: JobSearchQuery) -> list[dict]:
    """Trigger a job search via n8n webhook.

    Args:
        query: JobSearchQuery containing search terms, location, and max results.

    Returns:
        List of job dictionaries from the n8n webhook response.

    Raises:
        httpx.HTTPStatusError: If the webhook request fails.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.n8n_job_search_webhook_url,
            params=query.model_dump(mode="json"),
        )
        response.raise_for_status()
        return response.json()
