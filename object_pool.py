import game_world

# 각종 객체 풀링을 담당하는 클래스
# 객체 풀링 대상: 적, VFX, 발사체

class object_pool:
    def __init__(self):
        self.pool = {}

    def get_object(self, obj_class, *args, **kwargs):
        # unique_key: 오브젝트 summoner, 오브젝트 생성 위치 등 조건 구분
        unique_key = kwargs.get('unique_key', None)
        class_pool = self.pool.setdefault(obj_class, [])

        # unique_key가 있으면 같은 키의 활성화된 객체가 있는지 확인
        if unique_key:
            for obj in class_pool:
                # 키가 같고 이미 활성화된 객체가 있으면 해당 객체 지속 사용
                if not obj.inactive and getattr(obj, 'unique_key', None) == unique_key:
                    return obj

        # 조건 없이 비활성화된 객체 탐색
        for obj in class_pool:
            if obj.inactive:
                obj.reactivate(*args)
                if unique_key:
                    obj.unique_key = unique_key
                return obj
        # 없거나 모두 사용 중이면 새로 생성
        obj = obj_class(*args)
        if unique_key:
            obj.unique_key = unique_key
        class_pool.append(obj)
        game_world.add_object(obj, obj.layer)
        return obj