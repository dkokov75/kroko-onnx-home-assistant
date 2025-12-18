# Home Assistant Add-on: Sherpa Onnx TTS/Kroko Onnx STT

## Kroko Onnx Streaming STT Models

This section explains how to download and run Kroko ONNX streaming speech-to-text (STT) models.

1. Install Requirements
First, install the required Python dependencies:

```
pip3 install -r requirements.txt
```

2. List and Download Kroko Models

A helper script, kroko_model_utils.py, is provided to list and download available Kroko models.

**List all available languages:**

```
./kroko_model_utils.py -l all
```

**List models for a specific language:**
Choose a language code (for example, EN) and list the available models:

```
./kroko_model_utils.py -l EN
```

Notes:
- The list includes both community (FREE) and commercial (PRO) models.
- **Community (FREE) models do not require a license key** to download or use.
- **Commercial (PRO) models require a valid license key.**
- To obtain a license key, register on the [Kroko.ai dashboard](app.kroko.ai)
- Make sure to note the model_id of the model you want to use and your license key in case of a commercial models; you will need those in the next step.

3. Download the Selected Model
Start downloading the model by running:

```
./kroko_model_utils.py -a EN --key <license_key> --model_id <model_id>
```

Once the download is complete, the model files will be available in the following directory:

```
models/stt/kroko_models
```

4. Build and Run with Docker

As a final step, build the Docker image and start the container:

```
docker compose up --build -d
```

Your Kroko Onnx streaming STT service should now be up and running. Ready to use!

## TTS Models

TTS Models are automatically downloaded from [TTS Model list on Github](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models) and put into `/tts-models`.

## Installation via the Wyoming Protocol

1. Open your Home Assistant instance.
2. Navigate to **Settings -> Devices & Services**.
3. In the bottom-right corner, click the **"Add Integration"**.
4. From the list, select Wyoming Protocol.
5. Follow the on-screen instructions to complete the setup.

## How to use

Once the installation is complete, the Kroko Onnx Streaming STT will be automatically discovered by Home Assistant.

To use it in Home Assistant, follow these steps:

1. Go to **Settings -> Voice Assistants**.
2. Click "Add Assistant".
3. Fill in the required details and, from the **Speech-to-text** dropdown, select **"Kroko Onnx Streaming STT"**.

Your setup is now complete, and you can start using Kroko ONNX Streaming STT with Home Assistant.