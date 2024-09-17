import os
import pickle as pkl
import json
import struct
import tensorflow as tf
import numpy as np


def save_to_pkl(x, file):
    folder = '/'.join(file.split('/')[:-1])
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(file, 'wb') as f:
        pkl.dump(x, f)

def save_to_json(x, file):
    folder = '/'.join(file.split('/')[:-1])
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(file, 'w') as f:
        json.dump(x, f, indent=4)

def load_pkl(file):
    with open(file, 'rb') as f:
        x = pkl.load(f)
    return x

def load_model_structure(filename):
    with open(filename, 'rb') as file:
        # Read and unpack the header
        header_format = '8s i'
        header_size = struct.calcsize(header_format)
        header = file.read(header_size)
        _, nlayers = struct.unpack(header_format, header)

        # Prepare to reconstruct the model
        model = tf.keras.Sequential()
        
        # Read and reconstruct each layer
        layer_format = '4s ii'
        for _ in range(nlayers):
            layer_info = file.read(struct.calcsize(layer_format))
            activation_code, num_inputs, num_outputs = struct.unpack(layer_format, layer_info)
           # print("read ",activation_code, num_inputs, num_outputs) 
            # Decide how to process based on activation_code
            if activation_code in [b'RELU', b'SIGM', b'LINE']:
                # Standard dense layers
                activation = {
                    b'RELU': 'relu',
                    b'SIGM': 'sigmoid',
                    b'LINE': 'linear',
                    b'NONE': None
                }.get(activation_code, 'linear')  # Default to linear if unknown code

               
                weights_size = num_inputs * num_outputs
                weights_format = f'{weights_size}f'
                weights = np.array(struct.unpack(weights_format, file.read(weights_size * 4)), dtype=np.float32).reshape((num_inputs, num_outputs))
    
                # Read biases
                biases_format = f'{num_outputs}f'
                biases = np.array(struct.unpack(biases_format, file.read(num_outputs * 4)), dtype=np.float32)
    
                # Create layer with weights and activation
                layer = tf.keras.layers.Dense(num_outputs, activation=activation, input_shape=(num_inputs,))
                
                model.add(layer)
                model.build(input_shape=(None, num_inputs))
                # Set weights manually
                layer.set_weights([weights, biases])



            elif activation_code == b'NORM':
                # Normalization layers
                mean_size = num_inputs  # Using num_inputs for mean size
                variance_size = num_outputs  # Using num_outputs for variance size

                mean_format = f'{mean_size}f'
                variance_format = f'{variance_size}f'
                
                mean = np.array(struct.unpack(mean_format, file.read(mean_size * 4)), dtype=np.float32)
                variance = np.array(struct.unpack(variance_format, file.read(variance_size * 4)), dtype=np.float32)


                # Define the Normalization layer
                layer = tf.keras.layers.Normalization(axis=-1)
                
                # Build the layer first so that it initializes the mean and variance
                layer.build(input_shape=(None, num_inputs))
                
                # Manually assign the mean and variance to the layer's internal variables
                layer.mean = tf.convert_to_tensor([mean], dtype=tf.float32)
                layer.variance = tf.convert_to_tensor([variance], dtype=tf.float32)

               # print("new norm ",activation_code, layer.mean, layer.variance) 
                model.add(layer)
      

            else:
                # Other layers could be handled here as needed
                continue

        # Read input and output names
        input_names_len = struct.unpack('i', file.read(4))[0]
        input_names_bytes = file.read(input_names_len)
        input_names = input_names_bytes.decode().split(',') if input_names_bytes else []

        output_names_len = struct.unpack('i', file.read(4))[0]
        output_names_bytes = file.read(output_names_len)
        output_names = output_names_bytes.decode().split(',') if output_names_bytes else []

        return model, input_names, output_names