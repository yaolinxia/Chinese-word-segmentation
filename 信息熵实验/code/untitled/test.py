def evaluate(pred,test):
    test_result = []
    N = len(test)
    p_index = 0
    t_index = 0

    p_count = 0
    t_count = 0

    correct = 0
    error = 0
    while p_index < len(pred) and t_index < N:
        p_seg = pred[p_index]
        t_seg = test[t_index]

        if p_seg == t_seg:
            correct += 1
            p_index += 1
            t_index += 1
            p_count += len(p_seg)
            t_count += len(t_seg)
            test_result.append({"word":t_seg,"correct":1})
        else:
            if p_count + len(p_seg) > t_count + len(t_seg):
                t_index += 1
                t_count += len(t_seg)
                test_result.append({"word":t_seg,"correct":0})
            elif p_count + len(p_seg) < t_count + len(t_seg):
                error += 1
                p_index += 1
                p_count += len(p_seg)
            else:
                error += 1
                p_index += 1
                t_index += 1
                p_count += len(p_seg)
                t_count += len(t_seg)
                test_result.append({"word":t_seg,"correct":0})



    precision = correct/(correct+error)
    recall = correct/N
    F = 2 * precision * recall / (precision + recall)

    return precision,recall,F,test_result


def test(raw_file,seg_file,test_file):
    with open(seg_file,"r") as seg:
        seg_list = seg.read().split("/")

    with open(test_file,"r") as test:
        test_list = test.read().split("/")

    print(seg_list)
    print(test_list)

    import jieba
    with open(raw_file,"r") as file:
        content = file.read()

    jie = list(jieba.cut(content))
    print("/".join(jie))
    evaluate(seg_list,test_list)
    evaluate(jie,test_list)

def similarity(pred,test):
    precision,recall,F,test_result= evaluate(pred,test)
    return recall,test_result