import io
import os
import base64
import zipfile
from lxml import etree
from .errors import UnsupportedBCFVersion
from bcf_api_xml.models import (
    Topic,
    Comment,
    Viewpoint,
    VisualizationInfo,
)


def check_bcf_version(file):
    bcf_version_tree = etree.parse(file)
    root = bcf_version_tree.getroot()
    version = root.get("VersionId")
    if version != "2.1":
        raise UnsupportedBCFVersion(
            f"version {version} is nor supported. Only BCF 2.1 is supported"
        )


def to_json(bcf_file):
    with zipfile.ZipFile(bcf_file, "r") as zip_ref:
        with zip_ref.open("bcf.version") as version_file:
            check_bcf_version(version_file)
        files = zip_ref.infolist()
        all_topics = []
        for file in files:
            if file.is_dir():
                # if zip has explicit directories, ignore them
                continue
            if file.filename.endswith("markup.bcf"):
                markup = file.filename
                topic_directory = os.path.dirname(file.filename) + "/"

                root = etree.fromstring(zip_ref.read(markup))
                xml_topic = root.find("Topic")
                topic = Topic.to_python(xml_topic)
                topic["comments"] = [
                    Comment.to_python(comment_xml) for comment_xml in root.findall("Comment")
                ]
                viewpoints = [
                    Viewpoint.to_python(viewpoint_xml)
                    for viewpoint_xml in root.findall("Viewpoints")
                ]
                for viewpoint in viewpoints:
                    if filename := viewpoint.pop("snapshot_filename", None):
                        file = io.BytesIO(zip_ref.read(topic_directory + filename))
                        file.name = filename
                        viewpoint["snapshot"] = {
                            "snapshot_type": os.path.splitext(filename)[1],
                            "snapshot_data": file,
                        }
                    if filename := viewpoint.pop("viewpoint_filename", None):
                        xml = etree.fromstring(zip_ref.read(topic_directory + filename))
                        viewpoint.update(**VisualizationInfo.to_python(xml))
                topic["viewpoints"] = viewpoints
                all_topics.append(topic)
    return all_topics
