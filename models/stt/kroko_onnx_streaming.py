import os
import logging
import kroko_onnx

_LOGGER = logging.getLogger("kroko_onnx_streaming")

def load(cli_args):
    kroko_key = os.getenv("KROKO_KEY")
    model_name = os.getenv("KROKO_STT_MODEL")
    model_path = f"/app/models/stt/kroko_models/{model_name}"

    _LOGGER.info(f"Loading follow Kroko model: {model_path}")

    recognizer = kroko_onnx.OnlineRecognizer.from_transducer(
        model_path=model_path,
        key=kroko_key,
        referralcode="",
        num_threads=1,
        provider="cpu",
        sample_rate=16000,
        decoding_method="modified_beam_search",
        blank_penalty=0.0,
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=20.0,
    )

    _LOGGER.info(f"The Kroko model is started!")

    return recognizer
