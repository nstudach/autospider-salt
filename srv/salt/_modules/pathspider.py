import salt
import subprocess
import datetime
import time

def _send_salt_event(component, suffix, finished,
        success, error = None, message = None):
    """Transmit an event to the salt master

    The event will be tagged 'mami/pathspider/<component>/<suffix>/<minion-id>'
    and will contain the vaules of finished, success, error and message.

    Arguments:
    component -- should be ('spider', 'upload', 'measurement')
    suffix -- should be in ('completed', 'failed', 'started')
    finished -- bool
    success -- bool
    error -- str (optional)
    message -- str (optional)
    """

    # this comunicates with the outside world, so we should use some protection
    assert component in ('spider', 'upload', 'measurement')
    assert suffix in ('failed', 'completed', 'started')
    assert type(finished) == bool
    assert type(success) == bool
    assert (error == None) or type(error) == str
    assert (message == None) or type(message) == str

    worker_id = __grains__['id']
    event_tag = 'mami/pathspider/{}/{}/{}'.format(component,suffix,worker_id)

    __salt__['event.send'](event_tag,
                            {'finished': finished,
                             'success': success,
                             'error': error,
                             'message': message})

def _execute_spider(inputstream, outputstream, errorstream, timeout):
    """Execute the Pathspider command

    The patspider executable will be executed. It will be allowed to run for a
    maximum of <timeout> seconds, after which it will be killed.

    Arguments:
    inputstream -- a stream (e.g. an opened file) to be connected to stdin
    outputstream -- a stream (e.g. an opened file) to be connected to stdout
    errortream -- a stream (e.g. an opened file) to be connected to stderr
    timeout -- int, specifying the maximum time pathspider may run in seconds
               set to 0 to disable
    """

    starttime = datetime.datetime.now()

    _send_salt_event('spider', 'started', finished = False, success = True)
    # run pathspider
    spider = subprocess.Popen("pathspider -i eth0 -w 50 ecn", shell = True, 
            stdout = outputstream, stdin = inputstream, stderr = errorstream)

    # Wait for the spider to finish, and make sure it does not take to long
    while spider.poll() == None:

        currenttime = datetime.datetime.now()
        timedelta = currenttime - starttime
        
        # never true if timeout is zero, because then timeout management is disabled.
        if timeout and timedelta > datetime.timedelta(seconds = timeout):
            _send_salt_event( 'spider', 'failed', finished = True,
                    success = False, error = "Pathspider timeout")
            return False
        
        time.sleep(10) 
            
    #return True if measurement was sucessfull
    if spider.returncode == 0:
        _send_salt_event('spider', 'completed', finished = True,
                success = True)
        return True
    else:
        _send_salt_event('spider', 'failed', finished = True,
                success = False, error = "Nonzero return value")
        return False

def run(inputfile, timeout = 0):
    """Execute a Pathspider measurement

    This function is exposed to salt.

    Arguments:
    inputfile -- str, path to Pathspider input file
    timout -- int, maximum runtime of Pathspider command, in seconds.
    """

    _send_salt_event('measurement', 'started', finished = False,
        success = True)
    
    timestring = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')

    # open al the files to feed to pathspider
    outfile = open('/var/pathspider/pathspider-stdout-' + timestring, 'w')
    errfile = open('/var/pathspider/pathspider-stderr-' + timestring, 'w')
    infile = open(inputfile, 'r')

    spider_success = _execute_spider(infile, outfile, errfile, timeout)

    # Looks like the meausrement failed, no point in going on...
    if spider_success == False:
        _send_salt_event('measurement', 'failed', finished = True,
                success = False, error = "Spider failed")
        return False

# TODO: Upload results to observatory
     
    _send_salt_event('measurement', 'completed', finished = True,
        success = True)
    return True
