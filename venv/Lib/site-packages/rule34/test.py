import rule34
import pytest
import os


def test_Sync():
    r34 = rule34.Sync()
    assert r34.l is not None
    assert r34.getImages("gay") is not None


def test_async():
    import asyncio
    loop = asyncio.get_event_loop()
    r34 = rule34.Rule34(loop)
    assert (len(loop.run_until_complete(r34.getImages("gay"))) == 100)


def test_postData():
    r34 = rule34.Sync()
    assert (r34.getPostData(1) is not None)


def test_URLGen():
    r34 = rule34.Sync()
    expectedString = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=50&tags=gay&deleted=show&rating:explicit"
    assert (r34.URLGen(tags="gay", limit=50, deleted=True) == expectedString)


def test_URLGenPIDLimit():
    r34 = rule34.Sync()
    try:
        r34.URLGen(tags="gay", PID=2001)
    except rule34.Request_Rejected:
        pass
    except Exception as e:
        raise rule34.SelfTest_Failed(e)


def test_URLGenReturnNone():
    r34 = rule34.Sync()
    assert r34.URLGen() is None


def test_Download():
    r34 = rule34.Sync()
    downloadURL = 'https://img.rule34.xxx/images/2003/b90ae3f67eaa30669939531292d90e55d58325af.jpg'
    name = r34.download(downloadURL)
    assert name is not None
    assert os.path.isfile(name)
    assert os.path.getsize(name) >= 76600
    os.unlink(name)


def test_DonwloadNameHandler():
    r34 = rule34.Sync()
    downloadURL = 'https://img.rule34.xxx/images/2003/b90ae3f67eaa30669939531292d90e55d58325af.jpg'
    names = []
    names.append(r34.download(downloadURL))
    names.append(r34.download(downloadURL))
    for name in names:
        assert name is not None
        assert os.path.isfile(name)
        assert os.path.getsize(name) >= 76600
        os.unlink(name)


def test_DownloadErrorCatch():
    r34 = rule34.Sync()
    downloadURL = 'https://img.rule34.xxx/borris/2003/b90ae3f67eaa30669939531292d90e55d58325af.jpg'
    try:
        name = r34.download(downloadURL)
        os.unlink(name)
    except rule34.Rule34_Error:
        pass
    except Exception as e:
        raise rule34.SelfTest_Failed(e)


def test_TotalImages():
    r34 = rule34.Sync()
    assert r34.totalImages("gay") > 1000

def test_imageGatherNew():
    r34 = rule34.Sync()
    assert (r34.getImages("straight") is not None)

def test_imageGatherNew_total():
    r34 = rule34.Sync()
    assert (len(r34.getImages("straight")) == 100)

def test_imageGatherNew_OverridePID():
    r34 = rule34.Sync()
    assert (r34.getImages("straight",
                             singlePage=True,
                             OverridePID=1) is not None)

def test_imageGatherNew_fuzzy():
    r34 = rule34.Sync()
    assert (r34.getImages("vore",
                             singlePage=True,
                             fuzzy=True) is not None)


def test_imageGatherNew_Contradiction():
    r34 = rule34.Sync()
    assert (r34.getImages("vore",
                             singlePage=False,
                             randomPID=True) is not None)


def test_imageGatherNew_nonExist():
    r34 = rule34.Sync()
    assert (r34.getImages("DNATESTMAGICCOODENOTHINGWILLRETURN") is None)


def test_imageGatherNew_rejectRequest():
    r34 = rule34.Sync()
    try:
        r34.getImages("straight", fuzzy=True, OverridePID=2001)
    except rule34.Request_Rejected:
        pass
    except Exception as e:
        raise rule34.SelfTest_Failed(e)
