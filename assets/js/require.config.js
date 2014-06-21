var require = {
    baseUrl: "/static",
    paths: {
        'codes': 'js/codes',
        'errors': 'js/errors',
        'jquery': 'jquery/dist/jquery.min',
        'radiu': 'radiu/radiu',
        'jquery.iframe-transport': 'jquery.iframe-transport/jquery.iframe-transport',
        'select2': 'select2/select2',
        'moment': 'moment/moment',
        'chart': 'js/ChartNew',

        'jquery.ui.core': 'jqueryui/ui/jquery.ui.core',
        'jquery.ui.mouse': 'jqueryui/ui/jquery.ui.mouse',
        'jquery.ui.widget': 'jqueryui/ui/jquery.ui.widget',
        'jquery.ui.sortable': 'jqueryui/ui/jquery.ui.sortable',

        'bootstrap': 'bootstrap/dist/js/bootstrap.min',
        'bootstrap-alert': 'bootstrap-alert/alert',
        'jquery-placeholder': 'jquery-placeholder/jquery.placeholder',
        'jquery.pnotify': 'pnotify/jquery.pnotify.min',
        'jquery.cookie': 'jquery.cookie/jquery.cookie',
        'jquery.serializeObject': 'jQuery.serializeObject/dist/jquery.serializeObject.min',
        'django-csrf-support': 'django-csrf-support/index',
        'parsley': 'parsleyjs/parsley',
        'underscore': 'underscore/underscore',
        'multiline': 'multiline/browser',
        'bootstrap-datetimepicker': "smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker.min"
    },
    shim: {
        'jquery-placeholder': {
            deps: ['jquery']
        },

        'jquery.ui.core': {
            deps: ['jquery']
        },
        'jquery.ui.widget': {
            deps: ['jquery', 'jquery.ui.core']
        },
        'jquery.ui.mouse': {
            deps: ['jquery', 'jquery.ui.widget']
        },
        'jquery.ui.sortable': {
            deps: ['jquery', 'jquery.ui.core', 'jquery.ui.mouse', 'jquery.ui.widget']
        },

        'jquery.serializeObject': {
            deps: ['jquery']
        },
        'select2': {
            deps: ['jquery']
        },
        'jquery.iframe-transport': {
            deps: ['jquery']
        },
        'bootstrap': {
            deps: ['jquery']
        },
        'jquery.cookie': {
            deps: ['jquery']
        },
        'parsley': {
            deps: ['jquery']
        },
        'bootstrap-datetimepicker': {
            deps: ['jquery', 'bootstrap']
        }
    }
};
