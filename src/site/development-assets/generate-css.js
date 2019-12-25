var gulp = require('gulp');

var autoprefixer = require('autoprefixer');
var postcss = require('gulp-postcss');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('css', function () {
    var plugins = [
        autoprefixer()
    ];

    return gulp
        .src('./scss/*.scss')
        .pipe(sourcemaps.init())
            .pipe(sass.sync().on('error', sass.logError))
            .pipe(postcss(plugins))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('../site-assets/css/'));
});

gulp.task('default', ['css']);
