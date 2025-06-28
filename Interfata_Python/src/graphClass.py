import dearpygui.dearpygui as dpg

class Graph:
    def __init__(self, data_length, pos, tag="", size=(0, 0)):
        """Initialize graph with two line series"""
        self.data_length = data_length
        self.x_data = list(range(self.data_length))
        self.y1_data = [0] * data_length
        self.y2_data = [0] * data_length
        self.pos = pos

        self.size = (500, 300) if size[0] == size[1] == 0 else size
        self.tag = f"graph_{id(self)}" if tag == "" else tag

        with dpg.window(label=self.tag, pos=self.pos):
            with dpg.plot(label=self.tag+"_line", height=self.size[1], width=self.size[0]):

                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.set_axis_limits(dpg.last_item(), 0, self.data_length)

                self.y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag=self.tag+"_y_axis_1")

                # Line 1
                self.series1_tag = dpg.generate_uuid()
                dpg.add_line_series(self.x_data, self.y1_data,
                                    label="Series 1", parent=self.y_axis,
                                    tag=self.series1_tag)

                # Line 2
                self.series2_tag = dpg.generate_uuid()
                dpg.add_line_series(self.x_data, self.y2_data,
                                    label="Series 2", parent=self.y_axis,
                                    tag=self.series2_tag)

    def update_graph(self, new_value_1=0, new_value_2=0):
        """Update both line series with new values"""
        self.y1_data.pop(0)
        self.y1_data.append(new_value_1)

        self.y2_data.pop(0)
        self.y2_data.append(new_value_2)

        dpg.set_value(self.series1_tag, [self.x_data, self.y1_data])
        dpg.set_value(self.series2_tag, [self.x_data, self.y2_data])

        # Calculate min and max across both series for Y-axis scaling
        combined = self.y1_data + self.y2_data
        min_axis_val = min(combined)
        max_axis_val = max(combined)
        marge = 1 if max_axis_val - min_axis_val == 0 else (max_axis_val - min_axis_val) / 10

        dpg.set_axis_limits(self.tag+"_y_axis_1",
                            min_axis_val - marge,
                            max_axis_val + marge)
