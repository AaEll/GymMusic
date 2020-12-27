
import asyncio
import threading


class Player():

  def __init__(self):
    pass

  def queue(self,content_path):
    pass

  def close(self):
    pass

  def reset(self):
    pass
  

def threaded(fn):
  def wrapper(*args, **kwargs):
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()
    return thread
  return wrapper

async def run_subprocess(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    
    """
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    """
    return proc, stdout, stderr

class MidiPlayer(Player):
  open_audio_cmd = "fluidsynth -i -a pulseaudio /usr/share/sounds/sf2/FluidR3_GM.sf2 {}"
  def __init__(self):
    super(MidiPlayer, self).__init__()
    self._sub_process = None # current subprocess
    self._lock = asyncio.Semaphore(value=1)
  
  def queue(self,content_path):
    self._queue(content_path)

  def reset(self):
    pass
  def close(self):
    pass

  def is_running(self):
    # returns None if running, 0 if not
    poll = self._sub_process.poll()
    return poll is None

  @threaded
  async def _queue(self,content_path):
    await self._lock.acquire()
    # create music process and await for it to finish
    _ = asyncio.run_subprocess(run(self.open_audio_cmd.format(content_path)))
    self._lock.release()



