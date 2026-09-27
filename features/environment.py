"""Behave environment hooks with Allure attachments."""
from __future__ import annotations

import os
from pathlib import Path

import allure

from configs import Config
from core import BaseClient, NoAuth
from utils import get_logger

logger = get_logger("behave")


def _get_or_create_client(context, service_name: str) -> BaseClient:
    if not hasattr(context, "client") or context.client is None:
        context.client = {}
    if service_name not in context.client:
        client = BaseClient(service_name=service_name)
        client.set_auth(NoAuth())
        context.client[service_name] = client
        logger.debug("Created BaseClient for '%s'", service_name)
    return context.client[service_name]


def _severity_from_tags(tags) -> str:
    tags = set(tags or [])
    if "smoke" in tags:
        return "critical"
    if "regression" in tags and "negative" in tags:
        return "minor"
    if "regression" in tags:
        return "normal"
    return "normal"


def before_all(context) -> None:
    Path("reports/allure-results").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    env = os.getenv("ENV", "dev")
    logger.info("=" * 72)
    logger.info("STARTING BEHAVE RUN | ENV=%s", env)
    logger.info("Base URLs: %s", Config.get("base_urls"))
    logger.info("=" * 72)
    context.faker_seed = None


def before_scenario(context, scenario) -> None:
    context.client = {}
    context.response = None
    context.last_user = None
    context.deleted_users = []
    context.scenario_name = scenario.name

    allure.dynamic.feature(scenario.filename)
    allure.dynamic.story(scenario.name)
    allure.dynamic.severity(_severity_from_tags(scenario.tags))
    allure.dynamic.title(scenario.name)

    logger.info("-" * 72)
    logger.info("STARTING SCENARIO: %s", scenario.name)
    if "smoke" in scenario.tags:
        logger.info("  [tag] smoke")
    if "negative" in scenario.tags:
        logger.warning("  [tag] negative-path scenario")


def before_step(context, step) -> None:
    context.current_step = step
    logger.debug("  STEP: %s %s", step.keyword, step.name)


def after_step(context, step) -> None:
    """Attach the last API response to the step (if applicable)."""
    resp = getattr(context, "response", None)
    if resp is None:
        return
    try:
        allure.attach(
            f"{resp.method} {resp.url}\nStatus: {resp.status_code}\nElapsed: {resp.elapsed_ms:.1f} ms",
            name=f"step_response_{step.name[:40]}",
            attachment_type=allure.attachment_type.TEXT,
        )
        if resp.body is not None:
            allure.attach(
                str(resp.body),
                name="response_body",
                attachment_type=allure.attachment_type.JSON,
            )
        if getattr(resp, "request_payload", None):
            allure.attach(
                str(resp.request_payload),
                name="request_payload",
                attachment_type=allure.attachment_type.JSON,
            )
    except Exception as exc:
        logger.warning("Allure attach failed: %s", exc)

    if step.status == "failed":
        logger.error("  STEP FAILED: %s %s", step.keyword, step.name)


def after_scenario(context, scenario) -> None:
    logger.info("FINISHED SCENARIO: %s | status=%s", scenario.name, scenario.status)
    if getattr(context, "client", None):
        for name, client in context.client.items():
            try:
                client.close()
                logger.debug("Closed client '%s'", name)
            except Exception as exc:
                logger.warning("Client close failed for %s: %s", name, exc)


def after_all(context) -> None:
    logger.info("=" * 72)
    logger.info("BEHAVE RUN COMPLETE")
    logger.info("=" * 72)