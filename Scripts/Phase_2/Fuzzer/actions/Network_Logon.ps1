param(
    [string]$Server,
    [string]$User,
    [string]$Password
)

net use "\\$Server\C$" /user:$User $Password
