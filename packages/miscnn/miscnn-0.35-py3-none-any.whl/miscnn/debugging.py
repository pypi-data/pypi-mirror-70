from data_loading.data_io import Data_IO
from data_loading.interfaces import *

interface = NIFTI_interface(pattern="case_0000[0-3]", channels=1, classes=3)
data_path = "/home/mudomini/projects/KITS_challenge2019/kits19/data.original/"
data_io = Data_IO(interface, data_path, delete_batchDir=True)

indices_list = data_io.get_indiceslist()
indices_list.sort()
print(indices_list)

# sample = data_io.sample_loader(indices_list[0], load_seg=True, load_pred=False)
# print(sample.img_data.shape, sample.details["spacing"])

# Specify subfunctions for preprocessing
from miscnn.processing.subfunctions import *
# sf = [Resampling((9,9,9)), Padding((32,32,32), shape_must_be_divisible_by=16)]
sf = [Normalization(mode="grayscale")]

from miscnn import Preprocessor
pp = Preprocessor(data_io, data_aug=None, batch_size=1, subfunctions=sf,
                  prepare_subfunctions=True, prepare_batches=False,
                  analysis="patchwise-crop", patch_shape=(16,16,16))

# # Initialize Keras Data Generator for generating batches
# from miscnn.neural_network.data_generator import DataGenerator
# dataGen = DataGenerator(indices_list[2:4], pp, training=True, validation=False,
#                         shuffle=False)
#
# for img, seg in dataGen:
#     print(img.min(), img.max())
#     #print(batch.shape)

from miscnn.neural_network.model import Neural_Network
model = Neural_Network(preprocessor=pp)

from miscnn.evaluation.cross_validation import split_folds, run_fold
split_folds(indices_list[0:3], k_fold=3)

for i in range(0,3):
    print("Running fold:", str(i))
    run_fold(0, model)

# model.train(indices_list[2:4], epochs=2, iterations=5, callbacks=[])

# model.evaluate(indices_list[0:1], indices_list[1:2], epochs=2, iterations=5)

# pred = model.predict(indices_list[2:3], direct_output=True)

# from miscnn.evaluation.cross_validation import cross_validation
# cross_validation(indices_list[0:3], model, k_fold=3, epochs=3, iterations=10,
#                  draw_figures=True, run_detailed_evaluation=False)

# import numpy as np
# print(np.asarray(pred).shape)

# sample = data_io.sample_loader("case_00000:#:89", load_seg=True, load_pred=True)
# print(sample.img_data.shape, sample.seg_data.shape, sample.pred_data.shape)

# from miscnn.processing.data_augmentation import Data_Augmentation
# data_aug = Data_Augmentation(cycles=1,
#                              scaling=False, rotations=False,
#                              elastic_deform=False, mirror=False,
#                              brightness=False, contrast=False,
#                              gamma=True, gaussian_noise=True)
#
# # data_aug.seg_augmentation = True
#
# from processing.subfunctions.normalization import Normalization
# from processing.subfunctions.clipping import Clipping
# from processing.subfunctions.resampling import Resampling
# from processing.subfunctions.resize import Resize
# sf = [Clipping(min=-100, max=500), Normalization(z_score=True), Resampling((3.22, 1.62, 1.62))]
#
# from processing.preprocessor import Preprocessor
# pp = Preprocessor(data_io, data_aug=data_aug, batch_size=2, subfunctions=sf,
#                   prepare_subfunctions=True, prepare_batches=False,
#                   analysis="patchwise-crop", patch_shape=(16,16,16))
# pp.patchwise_skip_blanks = False

# from neural_network.model import Neural_Network
# from neural_network.metrics import dice_soft, dice_weighted, dice_crossentropy
# from neural_network.architecture.unet.multiRes import Architecture
# unet_multiRes = Architecture()
# model = Neural_Network(preprocessor=pp, metrics=[dice_soft, dice_weighted([1,1,5])],
#                        batch_queue_size=2, workers=1, architecture=unet_multiRes)
#
# from miscnn.neural_network.model import Neural_Network
# from miscnn.neural_network.architecture.unet.standard import Architecture
# from miscnn.neural_network.metrics import tversky_crossentropy, dice_soft_loss, dice_crossentropy, tversky_loss
#
# from tensorflow.keras import backend as K
#
# unet_plain = Architecture()
# model = Neural_Network(preprocessor=pp,
#                        loss=tversky_crossentropy,
#                        metrics=[tversky_loss, dice_crossentropy, dice_soft_loss, K.categorical_crossentropy])

# model.model.summary()

# from keras.callbacks import ModelCheckpoint
# cb_model = ModelCheckpoint("submission_model.hdf5", monitor="loss",
#                         c   verbose=1, save_best_only=True, mode="min")

# model.train(indices_list[0:1], epochs=100, iterations=10, callbacks=[])

# model.dump("lol")
# model.load("lol")
#
# model.train(indices_list[0:1], epochs=3, iterations=10, callbacks=[])
#
# test = model.predict(indices_list[88:89], direct_output=True)
# print(test[0].shape)

# history = model.evaluate(training_samples=[indices_list[0]], validation_samples=[indices_list[1]],
#                          iterations=10)

# from miscnn.evaluation.split_validation import split_validation
# split_validation(indices_list[0:7], model, percentage=0.2, epochs=3, iterations=10)

# from miscnn.evaluation.detailed_validation import detailed_validation
# detailed_validation(indices_list, model, evaluation_path="evaluation")

# from utils.visualizer import visualize_sample
# for i in range(0, batches[0][0].shape[0]):
#     img = batches[0][0][i]
#     seg = batches[0][1][i]
#     visualize_sample(img, seg, str(i), "test")

# print(data_io.sample_loader(indices_list[88:89][0]).img_data.shape)
# test = model.predict(indices_list[88:89], direct_output=True)
# print(test[0].shape)

    # print(str(batch_img.shape) + "\t" + str(batch_seg.shape))
    # print(str(batch_img[1].shape) + "\t" + str(batch_seg[1].shape))

    # print(str(batch.shape))
    # from miscnn.utils.patch_operations import crop_patch
    # test = crop_patch(batch, pp.cache["slicer_" + str(indices_list[88])])
    # print(test.shape)

    # batch_seg = np.argmax(batch_seg, axis=-1)
    # batch_seg = np.reshape(batch_seg, batch_seg.shape + (1,))
    # visualize_sample(batch_img[0], batch_seg[0], str(i) + "_batch1", "visualization")
    # visualize_sample(batch_img[1], batch_seg[1], str(i) + "_batch2", "visualization")

# sample = data_io.sample_loader(indices_list[12])
# from miscnn.processing.subfunctions.resampling import Resampling
# # Create a resampling Subfunction to voxel spacing 3.22 x 1.62 x 1.62 mm
# sf_resample = Resampling((3.22, 1.62, 1.62))
# sf_resample.preprocessing(sample)
#
# from PIL import Image
# import numpy as np
# from miscnn.utils.patch_operations import slice_matrix, concat_matrices
# img_shape = sample.img_data.shape
#
# image_reshaped = np.reshape(sample.img_data, (137, 237, 237))
# for i in range(0, 137):
#     img = Image.fromarray(image_reshaped[i].astype('uint8'))
#     img.save("visualization/" + "vorher_" + str(i) + ".jpg")
#
# pp.patchwise_overlap = (0,0,0)
# patches_img = slice_matrix(sample.img_data, pp.patch_shape,
#                                    pp.patchwise_overlap,
#                                    pp.data_io.interface.three_dim)
#
# patches_img = np.stack(patches_img)
#
# image = concat_matrices(patches=patches_img,
#                         image_size=img_shape,
#                         window=pp.patch_shape,
#                         overlap=pp.patchwise_overlap,
#                         three_dim=pp.data_io.interface.three_dim)
# print(image.shape)
# image = np.reshape(image, image.shape[0:3])
#
# for i in range(0, 137):
#     img = Image.fromarray(image[i].astype('uint8'))
#     img.save("visualization/" + "nachher_" + str(i) + ".jpg")
