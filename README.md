# Frame Segment Selection 

An example [FiftyOne plugin](https://docs.voxel51.com/plugins/index.html) for selecting and viewing a segment of frames given a selected reference frame.

### Installation

If you haven't already,
[install FiftyOne](https://docs.voxel51.com/getting_started/install.html):

```shell
pip install fiftyone
```

Then install the plugin and its dependencies:

```shell
fiftyone plugins download https://github.com/allenleetc/select_frames_example
```

### Usage in the FiftyOne App

1. Load your dataset. Currently the plugin relies on two sample frames `scene` and `frame`. These fields are currently **hardcoded** and **must be present**. (These hardcoded fieldnames can be updated in the plugin!)

    The dataset should contain images sampled from videos. The `scene` and `frame` metadata fields indicate the sequence and frame number from acquisition.

2. Select a reference sample. The plugin will extract a sequence of frames containing this sample and its neighbors.

3. Select and run the **Select Frames** plugin from the Plugin Menu above the grid.

4. Select the position of the reference frame and the number of frames to include in the returned frame segment.

5. Press `Execute` and the plugin will return a dynamically-grouped view with the segment of interest. This can be viewed in the grid or in the Modal viewer as either a sequence of frames or as a rendered video!
