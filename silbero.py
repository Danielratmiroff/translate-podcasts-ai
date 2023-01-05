
#############################
# Silbero model
#############################

# import torch
# import zipfile
# import torchaudio
# from glob import glob

# device = torch.device('cpu')  # gpu also possible

# model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
#                                        model='silero_stt',
#                                        language='en',  # 'de', 'es'
#                                        device=device)

# # see function signature for details
# (read_batch, split_into_batches, read_audio, prepare_model_input) = utils

# # download a single file in any format compatible with TorchAudio
# torch.hub.download_url_to_file(
#     'https://opus-codec.org/static/examples/samples/speech_orig.wav', dst='speech_orig.wav', progress=True)

# test_files = glob('speech_orig.wav')
# batches = split_into_batches(test_files, batch_size=10)
# input = prepare_model_input(read_batch(batches[0]), device=device)

# output = model(input)

# for example in output:
#     print(decoder(example.cpu()))
