# Being_The_Fire_Final

Wildland fires pose an increasing threat in light of anthropogenic climate change. Fire-spread models play an underpinning role in many areas of research across this domain, from emergency evacuation to insurance analysis. We study paths towards advancing such models through deep reinforcement learning. Aggregating 21 fire perimeters from the Western United States in 2017, we construct 11-layer raster images representing the state of the fire area. A convolution neural network based agent is trained offline on one million sub-images to create a generalizable baseline for predicting the best action - burn or not burn - given the then-current state on a particular fire edge. A series of online, TD(0) Monte Carlo Q-Learning based improvements are made with final evaluation conducted on a subset of holdout fire perimeters. We examine the performance of the learned agent/model against the FARSITE fire-spread model.  We also make available a novel data set and propose more informative evaluation metrics for future progress.

Publication Site - Climate Change AI: https://www.climatechange.ai/papers/neurips2021/22

Presentation NeurIPS 2021: https://recorder-v3.slideslive.com/?share=53700&s=1b69b1d9-c838-4e0e-a58f-da1b9f024872
