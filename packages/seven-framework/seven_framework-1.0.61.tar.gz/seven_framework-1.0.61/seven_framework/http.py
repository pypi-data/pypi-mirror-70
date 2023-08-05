# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 21:32:43
@LastEditTime: 2020-05-15 20:27:22
@LastEditors: ChenXiaolei
@Description: 
"""
import requests


class HTTPHelper:
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
      >>> req
      <Response [200]>
    """
    @classmethod
    def get(self, url, params=None, headers=None, **kwargs):
        """
        @description: http get请求
        @param url: 网络http地址
        @param param: 请求参数(字典)
        @param headers: 请求headers设置(字典)
        @return: 请求结果
        @last_editors: ChenXiaolei
        """
        try:
            return requests.get(url=url,
                                params=params,
                                headers=headers,
                                **kwargs)
        except:
            print(f"get请求url:{url},params:{params}异常")
            return None

    @classmethod
    def post(self,
             url,
             data=None,
             headers={'Content-Type': 'application/x-www-form-urlencoded'},
             **kwargs):
        """
        @description: http post请求
        @param url: 网络http地址
        @param data: 请求参数(字典)
        @param headers: 请求headers设置(字典)
        @return: 请求结果
        @last_editors: ChenXiaolei
        """
        try:
            if hasattr(headers, "Content-Type") and headers["headers"].find("json") > 0:
                return requests.post(url=url, json=data, headers=headers, **kwargs)
            return requests.post(url=url, data=data, headers=headers, **kwargs)
        except:
            print(f"get请求url:{url},params:{data}异常")
            return None
