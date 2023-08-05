"""Runs test jobs in serial."""
import subprocess

import yaml
from .config import run_config_filename

from pysperf import options
from pysperf.model_library import models, requires_model_stats
from .run_manager import _load_run_config, get_run_dir, get_time_limit_with_buffer, this_run_config


@requires_model_stats
def execute_run():
    # Read in config
    # Start executing the *.sh files
    this_run_dir = get_run_dir()
    _load_run_config(this_run_dir)
    jobs = this_run_config.jobs_to_run
    for jobnum, (model_name, solver_name) in enumerate(jobs, start=1):
        current_run_num = options["current run number"]
        print(f"Executing run {current_run_num}-{jobnum}/{len(jobs)}: Solver {solver_name} with model {model_name}.")
        runner_script = this_run_dir.joinpath(solver_name, model_name, "run_job.sh")
        try:
            subprocess.run(
                str(runner_script.resolve()),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=get_time_limit_with_buffer(models[model_name].build_time)
            )
        except subprocess.TimeoutExpired:
            pass
