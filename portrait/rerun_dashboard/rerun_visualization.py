# # %%
# import rerun as rr
# import rerun.blueprint as rrb


# def init_rerun():
#     blueprint = rrb.Blueprint(
#         rrb.Tabs(
#             rrb.Grid(
#                 rrb.Vertical(
#                     rrb.Horizontal(
#                         rrb.BarChartView(
#                             origin="/bar/0",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/1",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/2",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/3",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/4",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/5",
#                         ),
#                         rrb.BarChartView(
#                             origin="/bar/6",
#                         ),
#                     ),
#                     rrb.TimeSeriesView(
#                         origin="/loss",
#                         # contents="+ $/loss/**"
#                     )
#                 )
#             ),
#             rrb.Horizontal(
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/0/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/0/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/0/y"
#                     ),
#                 ),
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/1/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/1/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/1/y"
#                     ),
#                 ),
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/2/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/2/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/2/y"
#                     ),
#                 ),
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/3/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/3/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/3/y"
#                     ),
#                 ),
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/4/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/4/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/4/y"
#                     ),
#                 ),
#                 rrb.Vertical(
#                     rrb.TextDocumentView(
#                         origin="/5/text"
#                     ),
#                     rrb.BarChartView(
#                         origin="/5/x"
#                     ),
#                     rrb.BarChartView(
#                         origin="/5/y"
#                     ),
#                 ),
#             )
#             # rrb.Horizontal(
#             #     rrb.TensorView(
#             #         origin="/tensor/0"
#             #     ),
#             #     rrb.TensorView(
#             #         origin="/tensor/1"
#             #     ),
#             #     rrb.TensorView(
#             #         origin="/tensor/2"
#             #     ),
#             # )
#         )
#     )

#     rr.init("rerun_example_my_data_12", spawn=True)
#     rr.send_blueprint(blueprint, make_active=True)


# # init_rerun()
