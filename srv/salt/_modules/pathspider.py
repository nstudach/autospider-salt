import salt
import subprocess
import datetime
import time
import shlex

def _send_salt_event(component, suffix, finished,
        success, error = None, message = None):
    """
    Transmit an event to the salt master

    The event will be tagged 'mami/pathspider/<component>/<suffix>/<minion-id>'
    and will contain the vaules of finished, success, error and message.

    :type component: str
    :type suffix: str
    :param bool finished: Indicate if the event signifies that something was
                     fininshed
    :param bool success: Indicate if the the action was succesfull
    :param str error: Name of the error that occured
    :param bool message: Extra information about the event
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

def _execute_spider(inputfile, outputfile, errorfile,
        timeout=0, pathspider_args = []):
    """
    Execute the Pathspider command

    The patspider executable will be executed. It will be allowed to run for a
    maximum of <timeout> seconds, after which it will be killed.

    :param file inputfile: a file object to be attached to stdin of pathspider 
    :param file outputfile: a file object to be connected to stdout
    :param file errorfile:  a file ojbect to be connected to stderr
    :param int timeout: maximum time in seconds to wait for pathspider to return
                        if set to zero, we will wait forever
    """

    starttime = datetime.datetime.now()

    _send_salt_event('spider', 'started', finished = False, success = True)
    # run pathspider
    spider = subprocess.Popen(["pathspider"] + pathspider_args, 
    #spider = subprocess.Popen("pathspider -i eth0 -w 50 ecn", shell=True 
            stdout = outputfile, stdin = inputfile, stderr = errorfile)

    # Wait for the spider to finish, and make sure it does not take to long
    while spider.poll() == None:

        currenttime = datetime.datetime.now()
        timedelta = currenttime - starttime
        
        # never true if timeout is zero, 
        # because then timeout management is disabled.
        if timeout and timedelta > datetime.timedelta(seconds = timeout):
            _send_salt_event( 'spider', 'failed', finished = True,
                    success = False, error = "Pathspider timeout")
            return False
        
        time.sleep(10) 
            
    # return True if measurement was sucessfull
    if spider.returncode == 0:
        _send_salt_event('spider', 'completed', finished = True,
                success = True)
        return True
    else:
        _send_salt_event('spider', 'failed', finished = True,
                success = False, error = "Nonzero return value")
        return False

def run(inputfile, argstring=None, timeout=0, debug=0):
    """
    Execute a Pathspider measurement

    This function is exposed to salt.

    :param str inputfile: path to Pathspider inputfile
    :param int timeout: maximum time in seconds to wait for pathspider to return
                        if set to zero, we will wait forever
    """

    _send_salt_event('measurement', 'started', finished = False,
        success = True)
    
    timestring = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')

    # open al the files to feed to pathspider
    outfile = open('/var/pathspider/pathspider-stdout-' + timestring, 'w')
    errfile = open('/var/pathspider/pathspider-stderr-' + timestring, 'w')
    infile = open(inputfile, 'r')

    #Set default arguments, and split them out if needed
    if argstring == None:
        argstring = "-i eth0 -w 50 ecn"
    pathspider_args = shlex.split(argstring)

    spider_success = _execute_spider(infile, outfile, errfile, timeout,
            pathspider_args)

    # Looks like the meausrement failed, no point in going on...
    if spider_success == False:
        _send_salt_event('measurement', 'failed', finished = True,
                success = False, error = "Spider failed")
        return False

# TODO: Upload results to observatory
     
    _send_salt_event('measurement', 'completed', finished = True,
            success = True)
    return True
