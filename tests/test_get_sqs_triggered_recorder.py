import pytest

from aws_xray_sqs_lambda_segment_shim import get_sqs_triggered_recorder
from aws_xray_sqs_lambda_segment_shim.exceptions import (
    InvalidMessageID,
    InvalidTraceHeader,
)


def sqs_record():
    return {
        "attributes": {
            "AWSTraceHeader": "Root=1-5759e988-bd862e3fe1be46a994272793;Parent=3995c3f42cd8ad8;Sampled=1"
        },
        "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
    }


@pytest.fixture(autouse=True)
def disable_boto3(monkeypatch):
    monkeypatch.delattr("botocore.session.Session.get_credentials")


def test_valid_record():
    recorder = get_sqs_triggered_recorder(
        record=sqs_record(),
        lambda_request_id="059f36b4-87a3-44ab-83d2-661975830a7d",
        lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        region="eu-west-1",
    )
    with recorder.in_segment() as segment:
        assert segment.aws == {
            "message_id": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "operation": "SendMessage",
            "region": "eu-west-1",
            "request_id": "059f36b4-87a3-44ab-83d2-661975830a7d",
        }


def test_bad_record_no_trace_header():
    with pytest.raises(InvalidTraceHeader):
        get_sqs_triggered_recorder(
            record={
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
            },
            lambda_request_id="059f36b4-87a3-44ab-83d2-661975830a7d",
            lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        )


def test_bad_record_no_message_id():
    with pytest.raises(InvalidMessageID):
        get_sqs_triggered_recorder(
            record={
                "attributes": {
                    "AWSTraceHeader": "Root=1-5759e988-bd862e3fe1be46a994272793;Parent=3995c3f42cd8ad8;Sampled=1"
                },
            },
            lambda_request_id="059f36b4-87a3-44ab-83d2-661975830a7d",
            lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        )
