"""Cas d'usage applicatifs orchestrant le domaine et l'infrastructure."""
from __future__ import annotations

import time
import uuid
from typing import Optional
from core.domain.entities import ToolRequestDto, ToolResponseDto, OperationStatus
from core.domain.ports import IOperationalAdapter


class ExecuteActionUseCase:
    """Exécute l'action demandée avec mesure de latence et capture d'erreurs."""

    def __init__(self, adapter: IOperationalAdapter):
        self.adapter = adapter

    def execute(self, request: ToolRequestDto) -> ToolResponseDto:
        start = time.time()
        op_id = f"op-{uuid.uuid4().hex[:8]}"
        try:
            raw = self.adapter.execute_operation(request.action, request.parameters)
            duration = round((time.time() - start) * 1000, 2)
            return ToolResponseDto(
                operation_id=op_id,
                action=request.action,
                status=OperationStatus.SUCCESS,
                payload=raw,
                execution_duration_ms=duration
            )
        except Exception as e:
            duration = round((time.time() - start) * 1000, 2)
            return ToolResponseDto(
                operation_id=op_id,
                action=request.action,
                status=OperationStatus.FAILED,
                payload={},
                execution_duration_ms=duration,
                error_message=str(e)
            )
