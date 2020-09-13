import json
import os
from pathlib import Path
import azure.functions as func


def main(req: func.HttpRequest, inputblob: func.InputStream) -> func.HttpResponse:)
    data = json.loads(inputblob.read().decode())
    result = DatasetValidator.validate(data)
    if result:
        return func.HttpResponse(
                'Dataset is valid',
                status_code=200
        )
    else:
        return func.HttpResponse(
                'Dataset is invalid',
                status_code=200
        )



class DatasetValidator:
    """
    현대자동차 로보틱스에서 제공받은 데이터셋을 사전 검증한다.∂

    검증 절차
    1. person 이 포함된 이미지 수가 일치하는지?
    2. person 어노테이션 수가 일치하는지?
    https://www.notion.so/aimmo/Face-Annotation-8fe73c6c11c544ba94627a954070594b

    person의 category_id = 1

    결과 데이터
            이미지 수  어노테이션 수
    train	64115	262465
    Val	    2693	11004
    total	66808	273469
    """

    total_person_image_count = 2693
    total_person_annotation_count = 11004

    @classmethod
    def validate(cls, value):
        total_image_count = 0
        total_annotation_count = 0

        annotations = value.get('annotations')
        image_count = cls._count_images(annotations)
        annotation_count = cls._count_annotations(annotations)

        total_image_count += image_count
        total_annotation_count += annotation_count

        if total_image_count != cls.total_person_image_count:
            print('total number of person image count is invalid')
            return False

        if total_annotation_count != cls.total_person_annotation_count:
            print('total number of person annotation count is invalid')
            return False

        print('-- DATASET IS VALID --')

        return True


    @classmethod
    def _count_images(cls, annotations):
        unique_image_ids = set()

        for annotation in annotations:
            if annotation.get('category_id') == 1:
                image_id = annotation.get('image_id')
                unique_image_ids.add(image_id)

        return len(unique_image_ids)

    @classmethod
    def _count_annotations(cls, annotations):
        count = 0
        for annotation in annotations:
            if annotation.get('category_id') == 1:
                count += 1

        return count
