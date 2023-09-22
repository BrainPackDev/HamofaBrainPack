{
    "name": "Brainpack project timesheet time control",
    "version": "16.0.1.0.0",
    "category": "Project",
    "author": "BrainPack",
    "website": "https://www.brainpack.io",
    "depends": [
        "hr_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_line_view.xml",
        "views/project_project_view.xml",
        "views/project_task_view.xml",
        "wizards/hr_timesheet_switch_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    # "post_init_hook": "post_init_hook",
}
