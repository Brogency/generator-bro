from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # self.children.append(modules.ModelList(
        #     title='Example',
        #     column=1,
        #     collapsible=True,
        #     models=('apps.example_app.models.*',)
        # ))
