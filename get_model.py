import os
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import Input, Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint

def save_model(model):
    model_dir = "Data/Model/"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, "model.h5")
    model.save(model_path)
    print('Model saved to', model_path)

def get_model():
    inputs = Input(shape=(150, 150, 3))

    x = Conv2D(32, (3, 3), activation='relu')(inputs)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(4, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=outputs)

    optimizer = Adam(lr=0.001)  # Verwendung von Adam-Optimizer mit Lernrate 0.001
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

if __name__ == '__main__':
    model = get_model()
    
    # Speichern des besten Modells während des Trainings
    checkpoint_path = "Data/Model/best_model.h5"
    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    
    # Trainieren des Modells
    # Hier sollte der Code zur Bereitstellung von Trainingsdaten und zum Aufrufen von model.fit() eingefügt werden
    
    # Speichern des endgültigen Modells
    save_model(model)
