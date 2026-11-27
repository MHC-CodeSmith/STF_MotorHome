"""Run a CFD stage and stop clearly divergent solutions while preserving logs."""

import math
import re
import subprocess
import time


def run(command, env, log, timeout_s, guard=False):
    started = time.monotonic()
    reason = None
    with log.open("x") as stream:
        proc = subprocess.Popen(
            command,
            env=env,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        while proc.poll() is None:
            elapsed = time.monotonic() - started
            if elapsed > timeout_s:
                reason = "stage_timeout"
            if guard and log.exists():
                with log.open("rb") as source:
                    source.seek(max(0, log.stat().st_size - 500000))
                    text = source.read().decode(errors="replace")
                times = re.findall(r"^Time = ([0-9.eE+-]+)", text, re.MULTILINE)
                cds = re.findall(r"^\s*Cd:\s+([^\s]+)", text, re.MULTILINE)
                if cds:
                    value = float(cds[-1])
                    if not math.isfinite(value):
                        reason = "nonfinite_force_coefficient"
                    elif times and float(times[-1]) > 100 and abs(value) > 10:
                        # A broad failure guard, never a target Cd or convergence test.
                        reason = "gross_force_divergence_after_startup"
            if reason:
                import os
                import signal

                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                break
            time.sleep(5)
    return {
        "exit_code": proc.returncode,
        "elapsed_s": time.monotonic() - started,
        "stop_reason": reason,
    }
