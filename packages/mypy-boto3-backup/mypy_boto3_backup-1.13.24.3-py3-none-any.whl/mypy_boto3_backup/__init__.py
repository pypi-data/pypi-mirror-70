"""
Main interface for backup service.

Usage::

    ```python
    import boto3
    from mypy_boto3_backup import (
        BackupClient,
        Client,
    )

    session = boto3.Session()

    client: BackupClient = boto3.client("backup")
    session_client: BackupClient = session.client("backup")
    ```
"""
from mypy_boto3_backup.client import BackupClient, BackupClient as Client


__all__ = ("BackupClient", "Client")
