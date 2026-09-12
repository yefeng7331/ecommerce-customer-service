"""
@Author:叶枫
@Time:2026/9/11
@Desc: 意图识别模块验证
"""
from project.domain.state import DialogueState
from project.plan.models import TurnPlan, TurnPlanValidationResult, ClarifyReason, TaskTurnPlan
from project.task.command.models import StartFlowCommand, ResumeTaskCommand, CancelTaskCommand
from project.task.flow.models import FlowCatalog

"""
    这个模块是用户问题意图识别验证
    验证的目的是为了保证意图识别模块的正确性
    验证的手段是通过人工测试，人工测试的目的是为了保证意图识别模块的正确性
    便与降低大语言模型的幻觉和错误率
"""
class TurnPlanValidation:
    def validation(self,turn_plan:TurnPlan,
                   state:DialogueState,
                   flow_catalog:FlowCatalog
                   )->TurnPlanValidationResult:
        # 1判断意图识别是否识别到多个轨道，比如有闲聊和任务流程
        active_tracks:list[str] = []
        if turn_plan.task is not None:
            active_tracks.append('task')
        if turn_plan.knowledge is not None:
            active_tracks.append('knowledge')
        if turn_plan.chitchat is not None:
            active_tracks.append('chitchat')

        # 判断active_tracks里面轨道的数量
        if not active_tracks: # 没有识别到轨道内容
            return TurnPlanValidationResult(
                valid=False,
                reason=ClarifyReason.MISSING_TRACK
            )

        # 识别多个轨道，校验失败
        if len(active_tracks)>1:
            return TurnPlanValidationResult(
                valid=False,
                reason=ClarifyReason.MULTIPLE_TRACKS
            )
        # 识别一个轨道，获取一条轨道数据
        if len(active_tracks)==1:
            track = active_tracks[0]
            if track == 'task':
                return self._validator_task_plan(turn_plan.task,
                                                 state,
                                                 flow_catalog)
            if track == 'knowledge':
                return self._validator_knowledge_plan()

            if track == "chitchat":
                return TurnPlanValidationResult(valid=True)


            # 2如果识别只是一个轨道，根据不同轨道做不同校验
            ## 任务流程专门校验

            ## 知识检索专门校验

    def _validator_task_plan(self, task:TaskTurnPlan, state:DialogueState, flow_catalog:FlowCatalog):
        if not task.commands:
            return TurnPlanValidationResult(
                valid=False,
                reason=ClarifyReason.INVALID_TASK_COMMAND
            )
        for command in task.commands:
            if isinstance(command,StartFlowCommand):
                flow_id = command.flow
                if flow_id not in flow_catalog.flows:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )
            if isinstance(command,ResumeTaskCommand):
                # 恢复前提条件
                # 获取要恢复的任务id
                task_id = command.task_id
                # 获取终端列表所有的任务id
                all_paused_ids = [paused.task_id for paused in state.tasks.paused]
                # 判断恢复任务id在列表中是否存在
                if task_id not in all_paused_ids:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )
            if isinstance(command,CancelTaskCommand):
                # 获取一下取消任务id
                task_id = command.task_id
                # 把中断列表中的所有任务id获取出来
                all_paused_ids = [paused.task_id for paused in state.tasks.paused]


                # 把当前活跃任务中的任务id获取出来
                if state.tasks.active:
                    all_paused_ids.append(state.tasks.active.task_id)
                # 判断取消任务id是否存在
                if task_id not in all_paused_ids:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )
        return TurnPlanValidationResult(
            valid=True,
        )


    def _validator_knowledge_plan(self):
        return TurnPlanValidationResult(
            valid=True,
        )
