import pytest

from aws_xray_sqs_lambda_segment_shim import SQSTriggeredXrayRecorder
from aws_xray_sqs_lambda_segment_shim.exceptions import ImmutableSegmentError


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


@pytest.fixture
def recorder():
    return SQSTriggeredXrayRecorder(
        record=sqs_record(),
        lambda_request_id="test_request_id",
        lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        region="eu-west-1",
    )


def test_init(recorder):
    base_segment = recorder.get_trace_entity()

    assert recorder.message_id == "059f36b4-87a3-44ab-83d2-661975830a7d"
    assert recorder.request_id == "test_request_id"
    assert (
        recorder.lambda_arn
        == "arn:aws:lambda:us-west-2:123456789012:function:my-function"
    )

    assert base_segment.aws == {
        "message_id": "059f36b4-87a3-44ab-83d2-661975830a7d",
        "operation": "SendMessage",
        "region": "eu-west-1",
        "request_id": "test_request_id",
    }


def test_begin_segment(recorder):
    with pytest.raises(ImmutableSegmentError):
        recorder.begin_segment(name="", traceid="", parent_id="", sampling=False)


def test_in_segment(recorder):
    with pytest.raises(ImmutableSegmentError):
        recorder.in_segment(name="", traceid="", parent_id="", sampling=False)
