from progress.bar import IncrementalBar


class LoadingBar(IncrementalBar):
    suffix = " %(percent)d%%  [%(index)d/%(max)d files]  [%(elapsed)d sec]  [~%(eta)d sec]"
