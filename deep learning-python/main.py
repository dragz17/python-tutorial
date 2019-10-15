# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 10:48:26 2018

@author: dragz17
"""

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout

#dummy_y = ['anjing', 'kucing']

#def baseline_model():
# create model
model = Sequential()
model.add(Flatten(input_shape=(32,32,3)))
model.add(Dense(200, input_dim=3072, activation='relu'))
model.add(Dropout(0.9))
model.add(Dense(200, activation='relu'))
model.add(Dropout(0.9))
model.add(Dense(200, activation='relu'))
model.add(Dropout(0.9))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255, 
                                   shear_range = 0.2, 
                                   zoom_range = 0.2, 
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('./train', 
                                                 target_size = (32, 32), batch_size = 32, class_mode = 'binary')
test_set = test_datagen.flow_from_directory('./test1', target_size = (32, 32), batch_size = 32, class_mode = 'binary')



model.fit_generator(training_set, steps_per_epoch = 24999, epochs = 100, validation_data = test_set, validation_steps = 12500)


#estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)

#kfold = KFold(n_splits=10, shuffle=True, random_state=None)
#results = cross_val_score(estimator, X, dummy_y, cv=kfold)
#print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
    

