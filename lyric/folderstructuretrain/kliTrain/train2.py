from keras.applications import VGG16
from keras_preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras import models
from keras import layers

#Load the VGG model
def run(tbatch_size, vbatch_size, epochno,lastLayerNeurons):
    image_size=150
    vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3))
    # Freeze the layers except the last 4 layers
    # froze the 4 end layers which were used to classify images, now these layers were basically the fully connected neural network layers of the vgg16 model used to classify images right after the flattened image was sent to this network
    for layer in vgg_conv.layers[:-4]:
        layer.trainable = False
    
    # Check the trainable status of the individual layers
    for layer in vgg_conv.layers:
        print(layer, layer.trainable)
        
    
    
    # Create the model
    model = models.Sequential()
    
    # Add the vgg convolutional base model
    model.add(vgg_conv)
    
    # Add new layers
    model.add(layers.Flatten())
    model.add(layers.Dense(1024, activation='relu'))
    # model.add(layers.Dense(512, activation='relu'))
    # model.add(layers.Dropout(0.5)) # I had a limited dataset I had to include dropout in the fully connected network to prevent overfitting on the data.
    model.add(layers.Dense(lastLayerNeurons, activation='softmax'))
    
    # Show a summary of the model. Check the number of trainable parameters
    model.summary()

    train_batchsize = tbatch_size
    val_batchsize = vbatch_size
    train_dir='train'
    validation_dir='validation'
    #ImageDataGenerator module from keras and added variations to the dataset like tilting or selective blurring and increased my dataset size for each class.
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    
    validation_datagen = ImageDataGenerator(rescale=1./255)

    # Change the batchsize according to system RAM
    train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(image_size, image_size),
            batch_size=train_batchsize,
            class_mode='categorical',
            shuffle=True)
    
    validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=(image_size, image_size),
            batch_size=val_batchsize,
            class_mode='categorical',
            shuffle=True)

    # Compile the model
    model.compile(loss='categorical_crossentropy',
                optimizer=optimizers.RMSprop(learning_rate=1e-6),
                metrics=['acc'])

    filepath="usr/bin/weights-improvement.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]

    # Train the model
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.samples/train_generator.batch_size ,
        epochs=epochno,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples/validation_generator.batch_size,
        verbose=1,
        callbacks=callbacks_list)

#Plot the training progress
# import matplotlib.pyplot as plt
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.savefig('model_accuracy.png')
# plt.clf()
# #plt.show()

# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.savefig('model_loss.png')

# Create a generator for prediction
# validation_generator = validation_datagen.flow_from_directory(
#         validation_dir,
#         target_size=(image_size, image_size),
#         batch_size=val_batchsize,
#         class_mode='categorical',
#         shuffle=False)
'''
import numpy as np
# Get the filenames from the generator
fnames = validation_generator.filenames
 
# Get the ground truth from generator
ground_truth = validation_generator.classes
 
# Get the label to class mapping from the generator
label2index = validation_generator.class_indices
 
# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())
 
# Get the predictions from the model using the generator
predictions = model.predict_generator(validation_generator, steps=validation_generator.samples/validation_generator.batch_size,verbose=1)
predicted_classes = np.argmax(predictions,axis=1)
 
errors = np.where(predicted_classes != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),validation_generator.samples))
'''    

