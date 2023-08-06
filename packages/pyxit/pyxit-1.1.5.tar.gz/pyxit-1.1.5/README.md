# pyxit

This code implements the core algorithms for Random subwindows extraction and Extra-Trees classifiers.
It is used by Cytomine DataMining applications: classification_validation, classification_model_builder, classification_prediction,
segmentation_model_builder and segmentation_prediction.
But it can be run without Cytomine on local data (using dir_ls and dir_ts arguments).

It is based on the following paper:

1) For image/object classification:
"Towards Generic Image Classification using Tree-based Learning: an Extensive Empirical Study".
Raphael Maree, Pierre Geurts, Louis Wehenkel.
Pattern Recognition Letters, DOI: 10.1016/j.patrec.2016.01.006, 2016. 


2) For image semantic segmentation:
Fast Multi-Class Image Annotation with Random Subwindows and Multiple Output Randomized Trees
Dumont et al., 2009
http://orbi.ulg.ac.be/handle/2268/12205

# Install
Simply: 
```
pip install pyxit
```
