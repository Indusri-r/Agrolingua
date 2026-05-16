# TODO - DL-only disease prediction

- [ ] Confirm current disease model loading logic in `model_stub.py`.
- [ ] Modify `_load_disease_model()` to prefer and load **only** `models/disease_model.keras` for inference.
- [ ] Ensure fallback heuristics are used only when the DL model truly fails to load.
- [ ] Re-run a direct `process_image(static/test_img.jpg)` test to confirm `model_used == 'Crop disease model'`.
- [ ] (Optional) Re-run `/analyze` integration test once server is running.

