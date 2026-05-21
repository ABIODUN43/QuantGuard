import logging

logger = logging.getLogger(__name__)


def record_analysis_job(analysis_id: str) -> None:
    logger.info("Queued post-analysis job for analysis_id=%s", analysis_id)


def record_report_job(report_id: str) -> None:
    logger.info("Queued report generation job for report_id=%s", report_id)
