<template>
    <section class="page">
        <div class="page-title">
            <div>
                <p>我的报名</p>
                <h2>查看已报名活动</h2>
            </div>
            <strong>已报名 {{ myActivities.length }}个活动</strong>
        </div>
        <table>
            <thead>
                <tr>
                    <th>活动名称</th>
                    <th>日期</th>
                    <th>地点</th>
                    <th>操作</th>
                </tr>
               </thead>

                <tbody>
                    <tr v-for="item in myActivities" :key="item.id">
                        <td>{{ item.name }}</td>
                        <td>{{ item.date }}</td>
                        <td>{{ item.place }}</td>
                        <td>
                            <button class="button danger small" type="button" @click="cancelSignup(item.id)">
                                取消报名
                            </button>
                        </td>
                    </tr>
                    <tr v-if="myActivities.length === 0">
                        <td colspan="4" class="empty-cell">暂无报名记录</td>
                    </tr>
                </tbody>  
        </table>
    </section>
</template>

<script setup>
   
    import { useActivities } from "../composables/useActivities"

    const { cancelSignup, myActivities} = useActivities()
</script>