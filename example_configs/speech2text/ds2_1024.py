import tensorflow as tf
from open_seq2seq.models import Speech2Text
from open_seq2seq.encoders import DeepSpeech2Encoder
from open_seq2seq.decoders import FullyConnectedCTCDecoder
from open_seq2seq.data import Speech2TextDataLayer
from open_seq2seq.losses import CTCLoss
from open_seq2seq.optimizers.lr_policies import poly_decay


base_model = Speech2Text

base_params = {
  "random_seed": 0,
  "use_horovod": False,
  "num_gpus": 8,
  "batch_size_per_gpu": 32,
  "iter_size": 4,

  "num_epochs": 50,

  "save_summaries_steps": 100,
  "print_loss_steps": 10,
  "print_samples_steps": 5000,
  "eval_steps": 5000,
  "save_checkpoint_steps": 1000,
  "logdir": "experiments/librispeech",

  "optimizer": "Momentum",
  "optimizer_params": {
    "momentum": 0.90,
  },
  "lr_policy": poly_decay,
  "lr_policy_params": {
    "learning_rate": 0.005,
    "power": 0.5,
  },
  "larc_params": {
    "larc_eta": 0.001,
  },
  "dtype": tf.float32,
  # weight decay
  "regularizer": tf.contrib.layers.l2_regularizer,
  "regularizer_params": {
    'scale': 0.0005
  },
  "initializer": tf.contrib.layers.xavier_initializer,

  "summaries": ['learning_rate', 'variables', 'gradients', 'larc_summaries',
                'variable_norm', 'gradient_norm', 'global_gradient_norm'],

  "encoder": DeepSpeech2Encoder,
  "encoder_params": {
    "conv_layers": [
      {
        "kernel_size": [11, 41], "stride": [2, 2],
        "num_channels": 32, "padding": "SAME"
      },
      {
        "kernel_size": [11, 21], "stride": [1, 2],
        "num_channels": 32, "padding": "SAME"
      },
    ],
    "num_rnn_layers": 4,
    "rnn_cell_dim": 1536,

    "use_cudnn_rnn": True,
    "rnn_type": "cudnn_gru",
    "rnn_unidirectional": True,

    "row_conv": True,
    "row_conv_width": 8,

    "n_hidden": 0,

    "dropout_keep_prob": 0.5,
    "activation_fn": tf.nn.relu,
    "data_format": "channels_first",
  },

  "decoder": FullyConnectedCTCDecoder,
  "decoder_params": {
    "use_language_model": False,

    # params for decoding the sequence with language model
    "beam_width": 512,
    "lm_weight": 2.0,
    "word_count_weight": 1.0,
    "valid_word_count_weight": 2.5,

    "decoder_library_path": "ctc_decoder_with_lm/libctc_decoder_with_kenlm.so",
    "lm_binary_path": "language_model/lm.binary",
    "lm_trie_path": "language_model/trie",
    "alphabet_config_path": "open_seq2seq/test_utils/toy_speech_data/vocab.txt",
  },
  "loss": CTCLoss,
  "loss_params": {},
}

train_params = {
  "data_layer": Speech2TextDataLayer,
  "data_layer_params": {
    "num_audio_features": 160,
    "input_type": "spectrogram",
    "augmentation": {'time_stretch_ratio': 0.05,
                     'noise_level_min': -90,
                     'noise_level_max': -60},
    "vocab_file": "open_seq2seq/test_utils/toy_speech_data/vocab.txt",
    "dataset_files": [
      "librivox-train-cut.csv",
    ],
    "shuffle": True,
  },
}

eval_params = {
  "data_layer": Speech2TextDataLayer,
  "data_layer_params": {
    "num_audio_features": 160,
    "input_type": "spectrogram",
    "vocab_file": "open_seq2seq/test_utils/toy_speech_data/vocab.txt",
    "dataset_files": [
      "data/librispeech/librivox-dev-clean.csv",
    ],
    "shuffle": False,
  },
}
