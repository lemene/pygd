# pygd
pygd是python版的plgd，用于辅助编写较大的流程脚本。


# 结构
Pipeline: 一个命令对应一个工程，例如scripts下面的racon_project
Command: 一个Pipeline支持多个命令，如RaconPipeline支持config和polish两个命令，简单命令使用python函数完成，复杂的命令一般需要构建Job。

Job: 对应作业，她有多种子类，可以组织成复杂的作业。

SerialJob: 包含多个子Job，Job之间串行完成。
ParallelJob：包含多个ScriptJob，Job之间可以并行。
ScriptJob：执行一个脚本语句，这些任务可以提交到cluster执行。
FunctionJob：本地执行Python函数。

Cluster：定义一个


|- Task
    |-

# 例子
## racon.py
racon.py是将minimap2+racon的polishing过程
racon.py将上述过程改为：
1. 用seqtk将reads分块。
2. 调用minimap2将分块后的reads比对到contigs上。
3. 合并比对结果。
4. 调用seqtk将contigs分块。
5. 调用racon，分别polish各个子块。
6. 合并polish结果。