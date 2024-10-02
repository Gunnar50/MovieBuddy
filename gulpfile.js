const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const cleanCSS = require('gulp-clean-css');
const rename = require('gulp-rename');


gulp.task('sass', function() {
  return gulp.src('src/scss/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename('index.min.css'))
    .pipe(gulp.dest('src/static/compiled'));
});

gulp.task('sass-watch', function() {
  gulp.watch('src/scss/**/*.scss', gulp.series('sass'));
});
