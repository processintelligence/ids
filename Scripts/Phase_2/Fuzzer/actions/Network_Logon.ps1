param(
    [string]$Server,
    [string]$User,
    [string]$Password
)
# acces denied? 
net use "\\$Server\C$" /user:$User $Password
