import os
from keras.callbacks import ModelCheckpoint, TensorBoard
from get_dataset import get_dataset
from get_model import get_model, save_model

epochs = 100
batch_size = 32  # Anpassung der Batch-Größe

def train_model(model, X_train, X_test, Y_train, Y_test):
    # Erstellung des Checkpoint-Callbacks
    checkpoint_path = 'Data/Checkpoints/best_weights.h5'
    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

    # Erstellung des TensorBoard-Callbacks
    log_dir = 'Data/Logs'
    tensorboard = TensorBoard(log_dir=log_dir, histogram_freq=1)

    # Training des Modells
    history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, Y_test), callbacks=[checkpoint, tensorboard])

    return model, history

def main():
    # Laden der Daten
    X_train, X_test, Y_train, Y_test = get_dataset()

    # Laden des Modells
    model = get_model()

    # Training des Modells
    trained_model, history = train_model(model, X_train, X_test, Y_train, Y_test)

    # Speichern des trainierten Modells
    save_model(trained_model)

    return trained_model, history

if __name__ == '__main__':
    main()
