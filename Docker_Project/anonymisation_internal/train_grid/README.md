## Hyperparameter tuning 

The script to run is in the `train_grid.ipynb`. 
The learning rate grid
values are (5e-5, 3e-5, 5e-6, 3e-6), the batch
size grid values are (8, 16) and the sequence length sizes are (128, 512). The best model is found
on the development set by using early stopping with the
patience of 10 epochs.