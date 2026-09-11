import { computed, ref } from "vue"

const currentUser = ref(null)

const activities = ref([
    {
        id: 1,
        name: "校园科技讲座",
        type: "讲座",
        date: "2026-05-20",
        place: "图书馆报告厅",
        limit: 80,
        intro: "了解人工智能现实中的应用",
        signed: false,
        checked: false
    },
    {
        id: 2,
        name: "志愿服务招募",
        type: "志愿",
        date: "2026-05-21",
        place: "学生服务中心",
        limit: 60,
        intro: "参与校园开发日志愿服务",
        signed: false,
        checked: false
    },
    {
        id: 3,
        name: "心里健康工作坊",
        type: "成长",
        date: "2026-05-22",
        place: "心理中心",
        limit: 40,
        intro: "通过小组活动学习压力调节和情绪管理方式",
        signed: false,
        checked: false
    }

])

export function useActivities() {
    const isStudent = computed(() => currentUser.value?.role === 'student')
    const isAdmin = computed(() => currentUser.value?.role === 'admin')

    const myActivities = computed(() => {
        return activities.value.filter((item) => item.signed)
    })



    function login(role, username) {
        currentUser.value = {
            name: username,
            role
        }
    }

    function logout() {
        currentUser.value = null
    }

    function findActivity(id){
        for(const activity of activities.value) {
            if (activity.id === Number(id)) {
                return activity
            }
        }
        return null
    }

    function signup(id) {
        const activity = activities.value.find((item) => 
            item.id === Number(id)
        )

        if(activity) {
            activity.signed = true
        }
    }

    function cancelSignup(id) {
        const activity = activities.value.find((item) => 
            item.id === Number(id)
        )

        if(activity) {
            activity.signed = false
        }
    }

    // 增加活动
    function addActivity(form) {
        const newActivity =  {
                id: Date.now(),
                name: form.name,
                type: form.type,
                date: form.date,
                place: form.place,
                limit: Number(form.limit),
                intro: form.intro,
                signed: false,
                checked: false
            }
        // unshift 把新增的活动放在最前面
        activities.value.unshift(newActivity)
    }

    //修改活动
    function updateActivity(form){
        const activity = findActivity(form.id)

        if(activity){
            activity.name = form.name
            activity.type = form.type
            activity.date = form.date
            activity.place = form.place
            activity.limit = Number(form.limit)
            activity.intro = form.intro
        }
    }

    //删除活动

    function deleteActivity(id){
        activities.value = activities.value.filter((activity) => activity.id !== Number(id))
    }

    return {
        currentUser,
        isStudent,
        myActivities,
        isAdmin,
        activities,
        login,
        logout,
        findActivity,
        signup,
        cancelSignup,
        addActivity,
        updateActivity,
        deleteActivity
    }

}