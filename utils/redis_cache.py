from settings import r
import pickle


def redis_register_split(index, ip, cookie_id, site):
    r.set(index + '-' + ip + '-' + site, cookie_id, ex=10)


def redis_retrieve_split(index, ip, site):
    return r.get(index + '-' + ip + '-' + site)


def redis_retrieve_join(ip, site):
    jointed_uuid = ''
    for i in range(1, 5):
        curr_split = redis_retrieve_split(str(i), ip, site)
        if curr_split is None:
            return None
        jointed_uuid += curr_split.decode('utf-8')
    return jointed_uuid


def redis_set_benchmark_recent_site(config_id, mode, site):
    r.set(config_id + '-' + mode, site, ex=60)


def redis_get_benchmark_recent_site(config_id, mode):
    return r.get(config_id + '-' + mode)
