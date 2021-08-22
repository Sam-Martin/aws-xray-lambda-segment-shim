import pytest
from aws_xray_sdk.core.exceptions.exceptions import SegmentNotFoundException
from aws_xray_sdk.core.models.subsegment import Subsegment
from aws_xray_sdk.core.models.trace_header import TraceHeader

from aws_xray_sqs_lambda_segment_shim import TriggeredXrayRecorder


@pytest.fixture(autouse=True)
def disable_boto3(monkeypatch):
    monkeypatch.delattr("botocore.session.Session.get_credentials")


@pytest.fixture
def recorder():
    return TriggeredXrayRecorder(
        trace_header=TraceHeader(
            root="1-5759e988-bd862e3fe1be46a994272793",
            parent="3995c3f42cd8ad8",
            sampled=1,
        ),
        trigger_metadata={"message_id": "059f36b4-87a3-44ab-83d2-661975830a7d"},
        lambda_request_id="test_request_id",
        lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        region="eu-west-1",
    )


def test_begin_segment(recorder):
    segment = recorder.begin_segment()

    assert segment.aws == {
        "message_id": "059f36b4-87a3-44ab-83d2-661975830a7d",
        "operation": "SendMessage",
        "region": "eu-west-1",
        "request_id": "test_request_id",
    }


def test_in_segment(recorder):
    with recorder.in_segment() as segment:
        assert segment.aws == {
            "message_id": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "operation": "SendMessage",
            "region": "eu-west-1",
            "request_id": "test_request_id",
        }
    with pytest.raises(SegmentNotFoundException):
        recorder.current_segment()


def test_begin_subsegment(recorder):
    recorder.begin_segment()
    subsegment = recorder.begin_subsegment("Test")
    assert isinstance(subsegment, Subsegment)


def test_in_subsegment(recorder):
    with recorder.in_segment() as segment:
        with recorder.in_subsegment("Test") as subsegment:
            assert isinstance(subsegment, Subsegment)
        assert segment.ref_counter.get_current() == 0
