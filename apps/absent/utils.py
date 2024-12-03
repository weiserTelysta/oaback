
def get_responder(request):
    user = request.user
    # 获取审批者
    if user.department.leader.uid == user.uid:
        if user.department.name == '董事会':
            responder = None
        else:
            responder = user.department.manager
    else:
        responder = user.department.leader
    return responder