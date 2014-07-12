module.exports = {
    baseUrl: ".",
    paths: {
        // dependencies
        'jquery': 'components/jquery/dist/jquery.min',
        'radiu': 'components/radiu/radiu',
        'jquery.iframe-transport': 'components/jquery.iframe-transport/jquery.iframe-transport',
        'select2': 'components/select2/select2',
        'moment': 'components/moment/moment',
        'jquery.ui.core': 'components/jqueryui/ui/jquery.ui.core',
        'jquery.ui.mouse': 'components/jqueryui/ui/jquery.ui.mouse',
        'jquery.ui.widget': 'components/jqueryui/ui/jquery.ui.widget',
        'jquery.ui.sortable': 'components/jqueryui/ui/jquery.ui.sortable',
        'when': "components/when",
        "backbone": "components/backbone",
        'bootstrap': 'components/bootstrap/dist/js/bootstrap.min',
        'bootstrap-alert': 'components/bootstrap-alert/alert',
        'jquery-placeholder': 'components/jquery-placeholder/jquery.placeholder',
        'jquery.pnotify': 'components/pnotify/jquery.pnotify.min',
        'jquery.cookie': 'components/jquery.cookie/jquery.cookie',
        'jquery.serializeObject': 'components/jQuery.serializeObject/dist/jquery.serializeObject.min',
        'django-csrf-support': 'components/django-csrf-support/index',
        'parsley': 'components/parsleyjs/parsley',
        'underscore': 'components/underscore/underscore',
        'bootstrap-datetimepicker': "components/smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker",
        'zh-CN': "./components/smalot-bootstrap-datetimepicker/js/locales/bootstrap-datetimepicker.zh-CN",
        'multiline': 'components/multiline/browser',

        //base modules
        'codes': 'assets/js/codes',
        'errors': 'assets/js/errors',
        'utils': 'assets/js/utils',
        'chart': 'assets/js/ChartNew',
        'modals': 'assets/js/modals',
        'formProto': 'assets/js/formProto',
        'formValidationProto': 'assets/js/formValidationProto',
        'simple-upload': 'assets/js/simple-upload',

        // app modules
        'login': 'base/js/login',
        'talk': 'backend/js/talk',
        'jobs': 'backend/js/jobs'
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
        }
    }
};
