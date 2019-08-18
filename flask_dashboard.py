import time

from flask import request, g, render_template
from flask.views import MethodView


class DashboardApiView(MethodView):
    def get(self):
        path = set()
        path_data = {}
        with open('path.tick', 'r') as f:
            tick_data = f.readlines()

        for tick in tick_data:
            path, start_time, spend_time = tick.split('\t')
            if not path in path_data:
                path_data[path] = {
                    "count": 0,
                    "spend_time": [],
                    "start_time": []
                }
            
            path_data[path]["count"] += 1
            path_data[path]["spend_time"].append(float(spend_time))
            path_data[path]["start_time"].append(float(start_time))

        render_dict = {
            "path": [],
            "count": []
        }
        
        for path in path_data:
            render_dict["path"].append(path)
            render_dict["count"].append(path_data[path]["count"])

        return render_template(
            'dashboard.html', **render_dict
        )


def mount_dashboard_to(app_or_blueprint, dashboard_path="/dashboard/"):
    # mount middleware
    @app_or_blueprint.before_request
    def _before_app():
        g._request_start_time = time.time()
    
    @app_or_blueprint.after_request
    def _after_app(response):
        g._request_end_time = time.time()
        # spend time $ms
        spend_time = (g._request_end_time - g._request_start_time) * 1000
        with open('path.tick', 'a+') as f:
            f.write(
                '{}\t{}\t{}\n'.format(
                    request.path, g._request_start_time, spend_time
                )
            )
        return response
    
    app_or_blueprint.add_url_rule(
        dashboard_path, view_func=DashboardApiView.as_view('flask-dashboard-view')
    )
    return app_or_blueprint