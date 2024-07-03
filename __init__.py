import fiftyone.operators as foo
import fiftyone.operators.types as types
from fiftyone import ViewField as F


SCENE_FIELD = 'scene'
FRAME_FIELD = 'frame'

class SelectFrames(foo.Operator):

    LABEL = "Select Frames"

    @property
    def config(self):
        return foo.OperatorConfig(
            name="select_frames",
            label=self.LABEL,
            dynamic=True,  
        )


    def resolve_input(self, ctx):
        inputs = types.Object()

        n_selected = len(ctx.selected)
        if n_selected == 0:
            error = types.Error(
                label="No sample selected",
                description="Please select a sample."
            )
            inputs.view("error", error)
            return types.Property(inputs, view=types.View(label=self.LABEL))
        
        elif n_selected > 1:
            warning = types.Warning(
                label="Multiple selections", 
                description="Multiple samples are selected. Using the first selected sample."
            )
            inputs.view("warning", warning)

        POSN_CHOICES = ['at start','centered','at end']
        dataset = ctx.dataset
        posn_choices = types.DropdownView()
        for field_name in POSN_CHOICES:
            posn_choices.add_choice(field_name, label=field_name)

        inputs.enum(
            'position',
            posn_choices.values(),
            required=True,
            label='Reference sample position',
            description='Position of selected sample in segment',
            view=posn_choices,
        )

        cprops = {'slider': {'min': 5, "max": 25, "step": 1, "default": 15}}
        inputs.define_property(
            "num_frames",
            types.Number(int=True, min=5, max=25),
            default=15,
            label="Number of Frames",
            view=types.SliderView(componentsProps={
                     "slider":cprops}),
        )

        return types.Property(inputs, view=types.View(label=self.LABEL))


    def execute(self, ctx):
        dataset = ctx.dataset
        selected = ctx.selected

        position = ctx.params.get("position", None)
        num_frames = ctx.params.get("num_frames", None)

        samp = dataset[selected[0]] # use first selected sample
        scene = samp[SCENE_FIELD] 
        frame = samp[FRAME_FIELD]

        if position=='at start':
            start_frame = frame
            end_frame = frame + num_frames
        elif position=='centered':
            start_frame = frame - num_frames//2
            end_frame = frame + num_frames//2
        else:
            start_frame = frame - num_frames
            end_frame = frame

        view_expr_scene = F(SCENE_FIELD)==scene
        view_expr_frame = (F(FRAME_FIELD)>=start_frame) & (F(FRAME_FIELD)<=end_frame)
        view = dataset.match(view_expr_scene & view_expr_frame) \
                      .group_by(SCENE_FIELD, order_by=FRAME_FIELD)
        
        ctx.trigger("set_view", {"view": view._serialize()})


def register(p):
    p.register(SelectFrames)
