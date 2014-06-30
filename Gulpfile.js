var path = require("path");
var gulp = require("gulp");
var chalk = require("chalk");
var less = require("gulp-less");
var uglify = require("gulp-uglify");
var _ = require("underscore");

var async = require("async");
var rjs = require("requirejs");
var pkgs = require("./pkgs");

gulp.task('rjs', function(callback) {
    function compile(packages, dir) {
        return function(callback) {
            async.eachSeries(packages, function(pkg, cb) {
                console.log(pkg);
                rjs.optimize(_.extend(pkgs, {
                    name: pkg,
                    optimize: "none",
                    out: "assets/js" + "/" + pkg + ".js"
                }), function() {
                    console.log(pkg, "done!");
                    cb();
                }, function(err) {
                    console.log(pkg, "error!");
                    cb(err);
                });
            }, function(err) {
                callback(err);
            });
        };
    }

    async.series([
        compile(["login"], "base/js"),
        compile(["talk", "pages"], "backend/js" )
    ], callback);
});

gulp.task('less', function() {
    return gulp.src(['base/less/*.less', 'backend/less/*.less'])
        .pipe(less({
            paths: [
                'assets/less',
                'components'
            ]
        }))
        .pipe(gulp.dest('assets/css'));
});

gulp.task('watch-less', function() {
    gulp.watch("**/*.less", ['less']);
});
