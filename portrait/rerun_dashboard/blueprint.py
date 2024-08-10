import rerun as rr
import rerun.blueprint as rrb

def get_dashboard_blueprint():
    blueprint = rrb.Blueprint(
        rrb.Vertical(
            rrb.Spatial2DView(
                origin="/image"
                ),
            rrb.Horizontal(
                rrb.BarChartView(
                    origin="/midi",
                ),
                rrb.TextDocumentView(
                    origin="/text",
                    # plot_legend=("")
                )
            )
        )
    )
    return blueprint